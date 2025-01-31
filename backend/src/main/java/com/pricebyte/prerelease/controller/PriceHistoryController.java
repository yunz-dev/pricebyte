package com.pricebyte.prerelease.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import com.pricebyte.prerelease.entity.PriceHistory;
import com.pricebyte.prerelease.repository.PriceHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/price-history")
public class PriceHistoryController {

    @Autowired
    private PriceHistoryRepository priceHistoryRepository;

    // Get all price histories
    @GetMapping("/")
    public ResponseEntity<?> getAllPriceHistories() {
        try {
            List<PriceHistory> priceHistories = priceHistoryRepository.findAll();
            return ResponseEntity.ok(priceHistories);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving price histories: " + e.getMessage());
        }
    }

    // Get price history by ID
    @GetMapping("/{id}")
    public ResponseEntity<?> getPriceHistoryById(@PathVariable Long id) {
        try {
            Optional<PriceHistory> priceHistory = priceHistoryRepository.findById(id);
            if (priceHistory.isPresent()) {
                return ResponseEntity.ok(priceHistory.get());
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Price history not found with id: " + id);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving price history: " + e.getMessage());
        }
    }

    // Get price history by store product ID
    @GetMapping("/store-product/{storeProductId}")
    public ResponseEntity<?> getPriceHistoryByStoreProduct(@PathVariable Long storeProductId) {
        try {
            List<PriceHistory> priceHistories = priceHistoryRepository.findPriceHistoryByStoreProduct(storeProductId);
            return ResponseEntity.ok(priceHistories);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving price history by store product: " + e.getMessage());
        }
    }

    // Get current price for a store product on a specific date
    @GetMapping("/store-product/{storeProductId}/current")
    public ResponseEntity<?> getCurrentPrice(@PathVariable Long storeProductId, 
                                           @RequestParam(required = false) String date) {
        try {
            LocalDate queryDate = (date != null) ? LocalDate.parse(date) : LocalDate.now();
            List<PriceHistory> currentPrices = priceHistoryRepository.findCurrentPriceByStoreProductAndDate(storeProductId, queryDate);
            
            if (currentPrices.isEmpty()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("No price history found for store product " + storeProductId + " on date " + queryDate);
            }
            
            return ResponseEntity.ok(currentPrices.get(0));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving current price: " + e.getMessage());
        }
    }

    // Create price history
    @PostMapping("/")
    public ResponseEntity<?> createPriceHistory(@RequestBody PriceHistory priceHistory) {
        try {
            PriceHistory savedPriceHistory = priceHistoryRepository.save(priceHistory);
            return ResponseEntity.ok(savedPriceHistory);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error creating price history: " + e.getMessage());
        }
    }

    // Update price history
    @PutMapping("/{id}")
    public ResponseEntity<?> updatePriceHistory(@PathVariable Long id, @RequestBody PriceHistory priceHistoryDetails) {
        try {
            Optional<PriceHistory> optionalPriceHistory = priceHistoryRepository.findById(id);
            if (optionalPriceHistory.isPresent()) {
                PriceHistory priceHistory = optionalPriceHistory.get();
                priceHistory.setStartDate(priceHistoryDetails.getStartDate());
                priceHistory.setEndDate(priceHistoryDetails.getEndDate());
                priceHistory.setPrice(priceHistoryDetails.getPrice());
                
                PriceHistory updatedPriceHistory = priceHistoryRepository.save(priceHistory);
                return ResponseEntity.ok(updatedPriceHistory);
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Price history not found with id: " + id);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error updating price history: " + e.getMessage());
        }
    }

    // Delete price history
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deletePriceHistory(@PathVariable Long id) {
        try {
            priceHistoryRepository.deleteById(id);
            return ResponseEntity.ok("Price history deleted successfully");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error deleting price history: " + e.getMessage());
        }
    }
}