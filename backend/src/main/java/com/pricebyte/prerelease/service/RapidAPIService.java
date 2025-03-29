package com.pricebyte.prerelease.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import com.pricebyte.prerelease.entity.Product;
import com.pricebyte.prerelease.entity.StoreProduct;
import com.pricebyte.prerelease.repository.ProductRepository;
import com.pricebyte.prerelease.repository.StoreProductRepository;
import reactor.core.publisher.Mono;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
public class RapidAPIService {

    private final WebClient webClient;
    private final ProductRepository productRepository;
    private final StoreProductRepository storeProductRepository;

    @Autowired
    public RapidAPIService(ProductRepository productRepository, StoreProductRepository storeProductRepository) {
        this.webClient = WebClient.builder().build();
        this.productRepository = productRepository;
        this.storeProductRepository = storeProductRepository;
    }

    public void fetchAndStoreProducts(String query) {
        // Fetch from Woolworths
        fetchFromAPI("https://woolworths-products-api.p.rapidapi.com/woolworths/product-search?query=" + query, "woolworths");

        // Fetch from Coles
        fetchFromAPI("https://coles-product-price-api.p.rapidapi.com/coles/product-search?query=" + query, "coles");

        // Add delay to respect rate limits
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void fetchFromAPI(String url, String store) {
        String apiKey = System.getenv("RAPIDAPI_KEY");
        if (apiKey == null) return;

        Mono<Map> response = webClient.get()
                .uri(url)
                .header("x-rapidapi-key", apiKey)
                .header("x-rapidapi-host", store.equals("woolworths") ?
                    "woolworths-products-api.p.rapidapi.com" : "coles-product-price-api.p.rapidapi.com")
                .retrieve()
                .bodyToMono(Map.class);

        response.subscribe(data -> {
            List<Map<String, Object>> results = (List<Map<String, Object>>) data.get("results");
            if (results != null) {
                for (Map<String, Object> item : results) {
                    saveProduct(item, store);
                }
            }
        });
    }

    private void saveProduct(Map<String, Object> item, String store) {
        String name = (String) item.get(store.equals("woolworths") ? "productName" : "productName");
        String brand = (String) item.get("productBrand");
        String priceStr = item.get("currentPrice").toString();
        double price = Double.parseDouble(priceStr);
        String size = (String) item.get("productSize");
        String url = (String) item.get("url");

        // Create or update product
        Product product = productRepository.findByName(name).orElse(new Product());
        if (product.getId() == null) {
            product.setName(name);
            product.setBrand(brand);
            product.setCategory("General");
            product.setSize(size);
            product.setCreatedAt(LocalDateTime.now());
            product.setUpdatedAt(LocalDateTime.now());
            product = productRepository.save(product);
        }

        // Create store product
        StoreProduct storeProduct = new StoreProduct();
        storeProduct.setProduct(product);
        storeProduct.setStore(store);
        storeProduct.setStoreProductId(String.valueOf(item.get("barcode") != null ? item.get("barcode") : item.get("productId")));
        storeProduct.setStoreName(name);
        storeProduct.setCurrentPrice(price);
        storeProduct.setProductUrl(url);
        storeProduct.setAvailability(true);
        storeProduct.setCreatedAt(LocalDateTime.now());
        storeProduct.setUpdatedAt(LocalDateTime.now());

        storeProductRepository.save(storeProduct);
    }
}