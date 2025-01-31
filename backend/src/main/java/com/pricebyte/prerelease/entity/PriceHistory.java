package com.pricebyte.prerelease.entity;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.time.LocalDate;

@Entity
@Table(name = "price_history")
public class PriceHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "start_date")
    private LocalDate startDate;
    
    @Column(name = "end_date")
    private LocalDate endDate;
    
    private Float price;
    
    // Many-to-one relationship with StoreProduct
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_product_id")
    @JsonIgnore
    private StoreProduct storeProduct;
    
    // Constructors
    public PriceHistory() {}
    
    public PriceHistory(LocalDate startDate, LocalDate endDate, Float price, StoreProduct storeProduct) {
        this.startDate = startDate;
        this.endDate = endDate;
        this.price = price;
        this.storeProduct = storeProduct;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public LocalDate getStartDate() { return startDate; }
    public void setStartDate(LocalDate startDate) { this.startDate = startDate; }
    
    public LocalDate getEndDate() { return endDate; }
    public void setEndDate(LocalDate endDate) { this.endDate = endDate; }
    
    public Float getPrice() { return price; }
    public void setPrice(Float price) { this.price = price; }
    
    public StoreProduct getStoreProduct() { return storeProduct; }
    public void setStoreProduct(StoreProduct storeProduct) { this.storeProduct = storeProduct; }
}
