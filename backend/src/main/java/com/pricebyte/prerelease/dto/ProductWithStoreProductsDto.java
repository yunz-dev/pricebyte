package com.pricebyte.prerelease.dto;

import java.util.List;

public class ProductWithStoreProductsDto {
    private Long id;
    private String name;
    private String brand;
    private String category;
    private Float size;
    private String unit;
    private String imageUrl;
    private String description;
    private List<StoreProductDto> storeProducts;
    
    public ProductWithStoreProductsDto() {}
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getBrand() { return brand; }
    public void setBrand(String brand) { this.brand = brand; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public Float getSize() { return size; }
    public void setSize(Float size) { this.size = size; }
    
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
    
    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public List<StoreProductDto> getStoreProducts() { return storeProducts; }
    public void setStoreProducts(List<StoreProductDto> storeProducts) { this.storeProducts = storeProducts; }
}