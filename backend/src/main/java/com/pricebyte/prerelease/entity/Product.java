package com.pricebyte.prerelease.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "product")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false)
    private String brand;
    @Column(nullable = false)
    private String category;
    @Column(nullable = false)
    private Float size;
    @Column(nullable = false)
    private String unit;
    
    @Column(name = "image_url", nullable = false)
    private String imageUrl;
    
    @Column(nullable = false)
    private String description;
    
    // One-to-many relationship with StoreProduct
    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<StoreProduct> storeProducts;
    
    // Constructors
    public Product() {}
    
    public Product(String name, String brand, String category, Float size, String unit, String imageUrl, String description) {
        this.name = name;
        this.brand = brand;
        this.category = category;
        this.size = size;
        this.unit = unit;
        this.imageUrl = imageUrl;
        this.description = description;
    }
    
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
    
    public List<StoreProduct> getStoreProducts() { return storeProducts; }
    public void setStoreProducts(List<StoreProduct> storeProducts) { this.storeProducts = storeProducts; }
}
