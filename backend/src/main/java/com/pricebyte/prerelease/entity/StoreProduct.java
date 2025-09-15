package com.pricebyte.prerelease.entity;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;

@Entity
@Table(name = "store_product")
public class StoreProduct {
    @Id
    @Column(name = "store_product_id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long storeProductId;
    
    private String store;
    
    @Column(name = "standard_price")
    private Float standardPrice;
    
    @Column(name = "product_url")
    private String productUrl;
    
    @Column(name = "is_active")
    private Boolean isActive;
    
    // Many-to-one relationship with Product
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id") // This references the product id
    @JsonIgnore
    private Product product;
    
    // One-to-many relationship with PriceHistory
    @OneToMany(mappedBy = "storeProduct", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonIgnore
    private List<PriceHistory> priceHistories;
    
    // Constructors
    public StoreProduct() {}
    
    public StoreProduct(String store, Float standardPrice, String productUrl, Boolean isActive, Product product) {
        this.store = store;
        this.standardPrice = standardPrice;
        this.productUrl = productUrl;
        this.isActive = isActive;
        this.product = product;
    }
    
    // Getters and Setters
    public Long getStoreProductId() { return storeProductId; }
    public void setStoreProductId(Long storeProductId) { this.storeProductId = storeProductId; }
    
    public String getStore() { return store; }
    public void setStore(String store) { this.store = store; }
    
    public Float getStandardPrice() { return standardPrice; }
    public void setStandardPrice(Float standardPrice) { this.standardPrice = standardPrice; }
    
    public String getProductUrl() { return productUrl; }
    public void setProductUrl(String productUrl) { this.productUrl = productUrl; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public Product getProduct() { return product; }
    public void setProduct(Product product) { this.product = product; }
    
    public List<PriceHistory> getPriceHistories() { return priceHistories; }
    public void setPriceHistories(List<PriceHistory> priceHistories) { this.priceHistories = priceHistories; }
}
