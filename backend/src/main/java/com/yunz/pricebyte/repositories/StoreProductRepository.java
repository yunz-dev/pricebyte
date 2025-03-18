package com.yunz.pricebyte.repositories;

import com.yunz.pricebyte.entities.StoreProduct;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StoreProductRepository extends JpaRepository<StoreProduct, Long> {
}