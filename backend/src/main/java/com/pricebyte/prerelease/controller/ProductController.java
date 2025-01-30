package com.pricebyte.prerelease.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import com.pricebyte.prerelease.entity.Product;
import com.pricebyte.prerelease.service.ProductService;
import com.pricebyte.prerelease.dto.ProductWithStoreProductsDto;
import com.pricebyte.prerelease.dto.UpdatePriceDto;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/product")
public class ProductController {

@Autowired
    private ProductService productService;

	// @GetMapping("/")
	// public String index() {
	// 	return "Greetings from Spring Boot!";
	// }
	//
	// @DeleteMapping("/")
	// public String index() {
	// }
	//
	@GetMapping("/")
	public List<Product> getAllProducts() {
    return this.productService.getAllProducts();
	}

	@PostMapping("/")
	public ResponseEntity<?> insertNewProduct(@RequestBody ProductWithStoreProductsDto productDto) {
    try {
      Product createdProduct = this.productService.createProductWithStoreProducts(productDto);
      return ResponseEntity.ok(createdProduct);
    } catch (Exception e) {
      e.printStackTrace();
      return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
        .body("Error creating product: " + e.getMessage());
    }
	}

	// Update price endpoint
	@PutMapping("/price")
	public ResponseEntity<?> updatePrice(@RequestBody UpdatePriceDto updatePriceDto) {
	    try {
	        boolean updated = this.productService.updateStoreProductPrice(
	            updatePriceDto.getProductId(), 
	            updatePriceDto.getStore(), 
	            updatePriceDto.getNewPrice()
	        );
	        
	        if (updated) {
	            return ResponseEntity.ok("Price updated successfully");
	        } else {
	            return ResponseEntity.status(HttpStatus.NOT_FOUND)
	                .body("Product or store not found");
	        }
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error updating price: " + e.getMessage());
	    }
	}

	// Get product by ID
	@GetMapping("/{id}")
	public ResponseEntity<?> getProductById(@PathVariable Long id) {
	    try {
	        Optional<Product> product = this.productService.getProductById(id);
	        if (product.isPresent()) {
	            return ResponseEntity.ok(product.get());
	        } else {
	            return ResponseEntity.status(HttpStatus.NOT_FOUND)
	                .body("Product not found with id: " + id);
	        }
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error retrieving product: " + e.getMessage());
	    }
	}

	// Get products by category
	@GetMapping("/category/{category}")
	public ResponseEntity<?> getProductsByCategory(@PathVariable String category) {
	    try {
	        List<Product> products = this.productService.getProductsByCategory(category);
	        return ResponseEntity.ok(products);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error retrieving products by category: " + e.getMessage());
	    }
	}

	// Get products by brand
	@GetMapping("/brand/{brand}")
	public ResponseEntity<?> getProductsByBrand(@PathVariable String brand) {
	    try {
	        List<Product> products = this.productService.getProductsByBrand(brand);
	        return ResponseEntity.ok(products);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error retrieving products by brand: " + e.getMessage());
	    }
	}

	// Search products by name
	@GetMapping("/search")
	public ResponseEntity<?> searchProductsByName(@RequestParam String name) {
	    try {
	        List<Product> products = this.productService.searchProductsByName(name);
	        return ResponseEntity.ok(products);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error searching products: " + e.getMessage());
	    }
	}

	// Update product
	@PutMapping("/{id}")
	public ResponseEntity<?> updateProduct(@PathVariable Long id, @RequestBody Product productDetails) {
	    try {
	        Product updatedProduct = this.productService.updateProduct(id, productDetails);
	        return ResponseEntity.ok(updatedProduct);
	    } catch (RuntimeException e) {
	        return ResponseEntity.status(HttpStatus.NOT_FOUND)
	            .body("Product not found with id: " + id);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error updating product: " + e.getMessage());
	    }
	}

	// Delete product
	@DeleteMapping("/{id}")
	public ResponseEntity<?> deleteProduct(@PathVariable Long id) {
	    try {
	        this.productService.deleteProduct(id);
	        return ResponseEntity.ok("Product deleted successfully");
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
	            .body("Error deleting product: " + e.getMessage());
	    }
	}
}
