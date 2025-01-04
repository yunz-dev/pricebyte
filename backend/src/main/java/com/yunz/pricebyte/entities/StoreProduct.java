package com.yunz.pricebyte.entities;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "store_products")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class StoreProduct {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    private String store;
    private double price;
    private double unitPrice;
    private double originalPrice;
    private boolean availability;
    private String productUrl;
    private String weight;
}
