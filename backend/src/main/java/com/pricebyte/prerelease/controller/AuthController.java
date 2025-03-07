package com.pricebyte.prerelease.controller;

import com.pricebyte.prerelease.dto.AuthResponse;
import com.pricebyte.prerelease.dto.LoginRequest;
import com.pricebyte.prerelease.dto.RegisterRequest;
import com.pricebyte.prerelease.entity.User;
import com.pricebyte.prerelease.service.UserService;
import com.pricebyte.prerelease.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtil jwtUtil;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest request) {
        try {
            User user = userService.registerUser(request.getUsername(), request.getEmail(), request.getPassword());
            String token = jwtUtil.generateToken(user.getUsername());
            return ResponseEntity.ok(new AuthResponse(token, user.getUsername()));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Registration failed: " + e.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        User user = userService.findByUsername(request.getUsername());
        if (user != null && userService.checkPassword(request.getPassword(), user.getPassword())) {
            String token = jwtUtil.generateToken(user.getUsername());
            return ResponseEntity.ok(new AuthResponse(token, user.getUsername()));
        }
        return ResponseEntity.badRequest().body("Invalid credentials");
    }
}