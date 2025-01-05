package com.yunz.pricebyte.services;

import com.yunz.pricebyte.entities.Product;
import com.yunz.pricebyte.entities.StoreProduct;
import com.yunz.pricebyte.repositories.ProductRepository;
import com.yunz.pricebyte.repositories.StoreProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final StoreProductRepository storeProductRepository;

    public ProductService(ProductRepository productRepository, StoreProductRepository storeProductRepository) {
        this.productRepository = productRepository;
        this.storeProductRepository = storeProductRepository;
    }

    public Product addProduct(Product product) {
        return productRepository.save(product);
    }

    public StoreProduct addStoreProduct(StoreProduct storeProduct) {
        return storeProductRepository.save(storeProduct);
    }

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }

    public void deleteStoreProduct(Long id) {
        storeProductRepository.deleteById(id);
    }
}
