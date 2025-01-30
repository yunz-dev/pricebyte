// StoreProductService.java
package com.pricebyte.prerelease.service;

import com.pricebyte.prerelease.entity.StoreProduct;
import com.pricebyte.prerelease.repository.StoreProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class StoreProductService {
    
    @Autowired
    private StoreProductRepository storeProductRepository;
    
    public List<StoreProduct> getAllStoreProducts() {
        return storeProductRepository.findAll();
    }
    
    public Optional<StoreProduct> getStoreProductById(Long id) {
        return storeProductRepository.findById(id);
    }
    
    public List<StoreProduct> getStoreProductsByStore(String store) {
        return storeProductRepository.findByStore(store);
    }
    
    public List<StoreProduct> getActiveStoreProducts() {
        return storeProductRepository.findByIsActive(true);
    }
    
    public List<StoreProduct> getStoreProductsByProductId(Long productId) {
        return storeProductRepository.findByProductId(productId);
    }
    
    public StoreProduct createStoreProduct(StoreProduct storeProduct) {
        return storeProductRepository.save(storeProduct);
    }
    
    public StoreProduct updateStoreProduct(Long id, StoreProduct storeProductDetails) {
        StoreProduct storeProduct = storeProductRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("StoreProduct not found with id: " + id));
        
        storeProduct.setStore(storeProductDetails.getStore());
        storeProduct.setStandardPrice(storeProductDetails.getStandardPrice());
        storeProduct.setProductUrl(storeProductDetails.getProductUrl());
        storeProduct.setIsActive(storeProductDetails.getIsActive());
        storeProduct.setProduct(storeProductDetails.getProduct());
        
        return storeProductRepository.save(storeProduct);
    }
    
    public void deleteStoreProduct(Long id) {
        storeProductRepository.deleteById(id);
    }
}

