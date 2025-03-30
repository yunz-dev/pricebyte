// ProductService.java
package com.pricebyte.prerelease.service;

import com.pricebyte.prerelease.entity.Product;
import com.pricebyte.prerelease.entity.StoreProduct;
import com.pricebyte.prerelease.entity.PriceHistory;
import com.pricebyte.prerelease.repository.ProductRepository;
import com.pricebyte.prerelease.repository.StoreProductRepository;
import com.pricebyte.prerelease.repository.PriceHistoryRepository;
import com.pricebyte.prerelease.dto.ProductWithStoreProductsDto;
import com.pricebyte.prerelease.dto.StoreProductDto;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;
import java.time.LocalDate;

@Service
@Transactional
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private StoreProductRepository storeProductRepository;
    
    @Autowired
    private PriceHistoryRepository priceHistoryRepository;

    @Autowired
    private RapidAPIService rapidAPIService;

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }
    
    public Optional<Product> getProductById(Long id) {
        return productRepository.findById(id);
    }
    
    public List<Product> getProductsByCategory(String category) {
        return productRepository.findByCategory(category);
    }
    
    public List<Product> getProductsByBrand(String brand) {
        return productRepository.findByBrand(brand);
    }
    
    public List<Product> searchProductsByName(String name) {
        List<Product> results = productRepository.findByNameContainingIgnoreCase(name);
        if (results.isEmpty()) {
            rapidAPIService.fetchAndStoreProducts(name);
            // Wait a bit for async processing
            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            results = productRepository.findByNameContainingIgnoreCase(name);
        }
        return results;
    }
    
    public Product createProduct(Product product) {
        return productRepository.save(product);
    }
    
    public Product updateProduct(Long id, Product productDetails) {
        Product product = productRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Product not found with id: " + id));
        
        product.setName(productDetails.getName());
        product.setBrand(productDetails.getBrand());
        product.setCategory(productDetails.getCategory());
        product.setSize(productDetails.getSize());
        product.setUnit(productDetails.getUnit());
        product.setImageUrl(productDetails.getImageUrl());
        product.setDescription(productDetails.getDescription());
        
        return productRepository.save(product);
    }
    
    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }
    
    public Product createProductWithStoreProducts(ProductWithStoreProductsDto productDto) {
        // Create and save the Product entity
        Product product = new Product(
            productDto.getName(),
            productDto.getBrand(), 
            productDto.getCategory(),
            productDto.getSize(),
            productDto.getUnit(),
            productDto.getImageUrl(),
            productDto.getDescription()
        );
        
        Product savedProduct = productRepository.save(product);
        
        // Create and save StoreProduct entities if they exist
        if (productDto.getStoreProducts() != null && !productDto.getStoreProducts().isEmpty()) {
            for (StoreProductDto storeProductDto : productDto.getStoreProducts()) {
                StoreProduct storeProduct = new StoreProduct(
                    storeProductDto.getStore(),
                    storeProductDto.getStandardPrice(),
                    storeProductDto.getProductUrl(),
                    storeProductDto.getIsActive(),
                    savedProduct
                );
                StoreProduct savedStoreProduct = storeProductRepository.save(storeProduct);
                
                // Create initial price history record with today's date
                LocalDate today = LocalDate.now();
                PriceHistory priceHistory = new PriceHistory(
                    today, // start date
                    today, // end date (initially same as start)
                    storeProductDto.getStandardPrice(), // initial price
                    savedStoreProduct
                );
                priceHistoryRepository.save(priceHistory);
            }
        }
        
        return savedProduct;
    }
    
    public boolean updateStoreProductPrice(Long productId, String store, Float newPrice) {
        // Find the store product for this product and store
        List<StoreProduct> storeProducts = productRepository.findById(productId)
            .map(Product::getStoreProducts)
            .orElse(null);
            
        if (storeProducts == null) {
            return false;
        }
        
        StoreProduct storeProduct = storeProducts.stream()
            .filter(sp -> sp.getStore().equalsIgnoreCase(store))
            .findFirst()
            .orElse(null);
            
        if (storeProduct == null) {
            return false;
        }
        
        LocalDate today = LocalDate.now();
        
        // Get current price history record (the one with end_date = today or latest)
        List<PriceHistory> currentPriceHistory = priceHistoryRepository.findCurrentPriceByStoreProductAndDate(
            storeProduct.getStoreProductId(), today);
            
        if (currentPriceHistory.isEmpty()) {
            // No current price history, create new one
            PriceHistory newPriceHistory = new PriceHistory(today, today, newPrice, storeProduct);
            priceHistoryRepository.save(newPriceHistory);
        } else {
            PriceHistory latestPrice = currentPriceHistory.get(0);
            
            if (latestPrice.getPrice().equals(newPrice)) {
                // Same price, extend end date
                latestPrice.setEndDate(today);
                priceHistoryRepository.save(latestPrice);
            } else {
                // Different price, close current record and create new one
                latestPrice.setEndDate(today.minusDays(1)); // End yesterday
                priceHistoryRepository.save(latestPrice);
                
                // Create new price history record
                PriceHistory newPriceHistory = new PriceHistory(today, today, newPrice, storeProduct);
                priceHistoryRepository.save(newPriceHistory);
            }
        }
        
        // Update the store product's standard price
        storeProduct.setStandardPrice(newPrice);
        storeProductRepository.save(storeProduct);
        
        return true;
    }
}

