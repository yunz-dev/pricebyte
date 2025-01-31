// PriceHistoryRepository.java
package com.pricebyte.prerelease.repository;

import com.pricebyte.prerelease.entity.PriceHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface PriceHistoryRepository extends JpaRepository<PriceHistory, Long> {
    List<PriceHistory> findByStoreProductStoreProductId(Long storeProductId);
    
    @Query("SELECT ph FROM PriceHistory ph WHERE ph.storeProduct.storeProductId = ?1 AND ph.startDate <= ?2 AND (ph.endDate IS NULL OR ph.endDate >= ?2)")
    List<PriceHistory> findCurrentPriceByStoreProductAndDate(Long storeProductId, LocalDate date);
    
    @Query("SELECT ph FROM PriceHistory ph WHERE ph.storeProduct.storeProductId = ?1 ORDER BY ph.startDate DESC")
    List<PriceHistory> findPriceHistoryByStoreProduct(Long storeProductId);
}


