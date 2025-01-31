package com.pricebyte.prerelease.dto;

public class StoreProductDto {
    private Long id;
    private String store;
    private Float standardPrice;
    private String productUrl;
    private Boolean isActive;
    
    public StoreProductDto() {}
    
    public StoreProductDto(String store, Float standardPrice, String productUrl, Boolean isActive) {
        this.store = store;
        this.standardPrice = standardPrice;
        this.productUrl = productUrl;
        this.isActive = isActive;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getStore() { return store; }
    public void setStore(String store) { this.store = store; }
    
    public Float getStandardPrice() { return standardPrice; }
    public void setStandardPrice(Float standardPrice) { this.standardPrice = standardPrice; }
    
    public String getProductUrl() { return productUrl; }
    public void setProductUrl(String productUrl) { this.productUrl = productUrl; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
}