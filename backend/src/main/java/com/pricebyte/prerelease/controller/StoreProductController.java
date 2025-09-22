package com.pricebyte.prerelease.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import com.pricebyte.prerelease.entity.StoreProduct;
import com.pricebyte.prerelease.repository.StoreProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/store-product")
@CrossOrigin(origins = "http://localhost:3000")
public class StoreProductController {

    @Autowired
    private StoreProductRepository storeProductRepository;

    // Get all store products
    @GetMapping("/")
    public ResponseEntity<?> getAllStoreProducts() {
        try {
            List<StoreProduct> storeProducts = storeProductRepository.findAll();
            return ResponseEntity.ok(storeProducts);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving store products: " + e.getMessage());
        }
    }

    // Get store product by ID
    @GetMapping("/{id}")
    public ResponseEntity<?> getStoreProductById(@PathVariable Long id) {
        try {
            Optional<StoreProduct> storeProduct = storeProductRepository.findById(id);
            if (storeProduct.isPresent()) {
                return ResponseEntity.ok(storeProduct.get());
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Store product not found with id: " + id);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving store product: " + e.getMessage());
        }
    }

    // Create store product
    @PostMapping("/")
    public ResponseEntity<?> createStoreProduct(@RequestBody StoreProduct storeProduct) {
        try {
            StoreProduct savedStoreProduct = storeProductRepository.save(storeProduct);
            return ResponseEntity.ok(savedStoreProduct);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error creating store product: " + e.getMessage());
        }
    }

    // Update store product
    @PutMapping("/{id}")
    public ResponseEntity<?> updateStoreProduct(@PathVariable Long id, @RequestBody StoreProduct storeProductDetails) {
        try {
            Optional<StoreProduct> optionalStoreProduct = storeProductRepository.findById(id);
            if (optionalStoreProduct.isPresent()) {
                StoreProduct storeProduct = optionalStoreProduct.get();
                storeProduct.setStore(storeProductDetails.getStore());
                storeProduct.setStandardPrice(storeProductDetails.getStandardPrice());
                storeProduct.setProductUrl(storeProductDetails.getProductUrl());
                storeProduct.setIsActive(storeProductDetails.getIsActive());
                
                StoreProduct updatedStoreProduct = storeProductRepository.save(storeProduct);
                return ResponseEntity.ok(updatedStoreProduct);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Store product not found with id: " + id);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error updating store product: " + e.getMessage());
        }
    }

    // Delete store product
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteStoreProduct(@PathVariable Long id) {
        try {
            storeProductRepository.deleteById(id);
            return ResponseEntity.ok("Store product deleted successfully");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error deleting store product: " + e.getMessage());
        }
    }
}