package com.yunz.pricebyte.repositories;

import com.yunz.pricebyte.entities.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {
}
