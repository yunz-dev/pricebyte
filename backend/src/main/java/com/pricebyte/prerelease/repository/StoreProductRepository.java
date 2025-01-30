// StoreProductRepository.java
package com.pricebyte.prerelease.repository;

import com.pricebyte.prerelease.entity.StoreProduct;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface StoreProductRepository extends JpaRepository<StoreProduct, Long> {
    List<StoreProduct> findByStore(String store);
    List<StoreProduct> findByIsActive(Boolean isActive);
    List<StoreProduct> findByProductId(Long productId);
    
    @Query("SELECT sp FROM StoreProduct sp WHERE sp.store = ?1 AND sp.isActive = true")
    List<StoreProduct> findActiveProductsByStore(String store);
}

