// PriceHistoryService.java
package com.pricebyte.prerelease.service;


import com.pricebyte.prerelease.entity.PriceHistory;
import com.pricebyte.prerelease.repository.PriceHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class PriceHistoryService {
    
    @Autowired
    private PriceHistoryRepository priceHistoryRepository;
    
    public List<PriceHistory> getAllPriceHistories() {
        return priceHistoryRepository.findAll();
    }
    
    public Optional<PriceHistory> getPriceHistoryById(Long id) {
        return priceHistoryRepository.findById(id);
    }
    
    public List<PriceHistory> getPriceHistoryByStoreProduct(Long storeProductId) {
        return priceHistoryRepository.findPriceHistoryByStoreProduct(storeProductId);
    }
    
    public List<PriceHistory> getCurrentPrice(Long storeProductId) {
        return priceHistoryRepository.findCurrentPriceByStoreProductAndDate(storeProductId, LocalDate.now());
    }
    
    public PriceHistory createPriceHistory(PriceHistory priceHistory) {
        return priceHistoryRepository.save(priceHistory);
    }
    
    public PriceHistory updatePriceHistory(Long id, PriceHistory priceHistoryDetails) {
        PriceHistory priceHistory = priceHistoryRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("PriceHistory not found with id: " + id));
        
        priceHistory.setStartDate(priceHistoryDetails.getStartDate());
        priceHistory.setEndDate(priceHistoryDetails.getEndDate());
        priceHistory.setPrice(priceHistoryDetails.getPrice());
        priceHistory.setStoreProduct(priceHistoryDetails.getStoreProduct());
        
        return priceHistoryRepository.save(priceHistory);
    }
    
    public void deletePriceHistory(Long id) {
        priceHistoryRepository.deleteById(id);
    }
}


