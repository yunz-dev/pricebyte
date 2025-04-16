package com.pricebyte.prerelease.repository;
import com.pricebyte.prerelease.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByCategory(String category);
    List<Product> findByBrand(String brand);
    List<Product> findByNameContainingIgnoreCase(String name);
    Optional<Product> findByName(String name);

    @Query("SELECT p FROM Product p WHERE p.category = ?1 AND p.brand = ?2")
    List<Product> findByCategoryAndBrand(String category, String brand);
}

