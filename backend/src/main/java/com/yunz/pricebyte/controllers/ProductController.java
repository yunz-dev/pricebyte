package com.yunz.pricebyte.controllers;

import com.yunz.pricebyte.entities.Product;
import com.yunz.pricebyte.entities.StoreProduct;
import com.yunz.pricebyte.services.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        return ResponseEntity.ok(productService.addProduct(product));
    }

    @PostMapping("/store")
    public ResponseEntity<StoreProduct> createStoreProduct(@RequestBody StoreProduct storeProduct) {
        return ResponseEntity.ok(productService.addStoreProduct(storeProduct));
    }

    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/store/{id}")
    public ResponseEntity<Void> deleteStoreProduct(@PathVariable Long id) {
        productService.deleteStoreProduct(id);
        return ResponseEntity.noContent().build();
    }
}
