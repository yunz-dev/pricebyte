package com.yunz.pricebyte.controllers;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/product")
public class ProductController2 {

    @GetMapping("/{id}")
    public int GetProduct(@PathVariable int id) {
        return id;
    }
}