package com.pricebyte.prerelease.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import com.pricebyte.prerelease.entity.Product;
import com.pricebyte.prerelease.service.ProductService;
import com.pricebyte.prerelease.dto.ProductWithStoreProductsDto;
import com.pricebyte.prerelease.dto.UpdatePriceDto;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import java.util.Optional;

class SearchResult {
    private Long id;
    private String name;
    private String brand;
    private String category;
    private String size;
    private String unit;
    private String image_url;
    private String description;
    private Double similarity_score;
    private String created_at;
    private String updated_at;

    public SearchResult(Long id, String name, String brand, String category, String size, String unit, String image_url, String description, Double similarity_score, String created_at, String updated_at) {
        this.id = id;
        this.name = name;
        this.brand = brand;
        this.category = category;
        this.size = size;
        this.unit = unit;
        this.image_url = image_url;
        this.description = description;
        this.similarity_score = similarity_score;
        this.created_at = created_at;
        this.updated_at = updated_at;
    }

    // Getters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getBrand() { return brand; }
    public String getCategory() { return category; }
    public String getSize() { return size; }
    public String getUnit() { return unit; }
    public String getImage_url() { return image_url; }
    public String getDescription() { return description; }
    public Double getSimilarity_score() { return similarity_score; }
    public String getCreated_at() { return created_at; }
    public String getUpdated_at() { return updated_at; }
}

class SearchResponse {
    private List<SearchResult> results;
    private int total_count;
    private int offset;
    private int limit;
    private boolean has_next;

    public SearchResponse(List<SearchResult> results, int total_count, int offset, int limit, boolean has_next) {
        this.results = results;
        this.total_count = total_count;
        this.offset = offset;
        this.limit = limit;
        this.has_next = has_next;
    }

    // Getters
    public List<SearchResult> getResults() { return results; }
    public int getTotal_count() { return total_count; }
    public int getOffset() { return offset; }
    public int getLimit() { return limit; }
    public boolean isHas_next() { return has_next; }
}