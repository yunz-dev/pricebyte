package com.pricebyte.prerelease.dto;

public class UpdatePriceDto {
    private Long productId;
    private String store;
    private Float newPrice;
    
    public UpdatePriceDto() {}
    
    public UpdatePriceDto(Long productId, String store, Float newPrice) {
        this.productId = productId;
        this.store = store;
        this.newPrice = newPrice;
    }
    
    // Getters and Setters
    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }
    
    public String getStore() { return store; }
    public void setStore(String store) { this.store = store; }
    
    public Float getNewPrice() { return newPrice; }
    public void setNewPrice(Float newPrice) { this.newPrice = newPrice; }
}