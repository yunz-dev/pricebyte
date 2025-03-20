package com.pricebyte.prerelease.controller;

import com.pricebyte.prerelease.dto.AuthResponse;
import com.pricebyte.prerelease.dto.LoginRequest;
import com.pricebyte.prerelease.dto.RegisterRequest;
import com.pricebyte.prerelease.entity.User;
import com.pricebyte.prerelease.service.UserService;
import com.pricebyte.prerelease.util.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AuthControllerTest {

    @Mock
    private UserService userService;

    @Mock
    private JwtUtil jwtUtil;

    @InjectMocks
    private AuthController authController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testRegisterSuccess() {
        RegisterRequest request = new RegisterRequest("testuser", "test@example.com", "password");
        User user = new User("testuser", "test@example.com", new BCryptPasswordEncoder().encode("password"));

        when(userService.registerUser("testuser", "test@example.com", "password")).thenReturn(user);
        when(jwtUtil.generateToken("testuser")).thenReturn("token");

        ResponseEntity<?> response = authController.register(request);

        assertEquals(200, response.getStatusCodeValue());
        AuthResponse authResponse = (AuthResponse) response.getBody();
        assertNotNull(authResponse);
        assertEquals("token", authResponse.getToken());
    }

    @Test
    void testLoginSuccess() {
        LoginRequest request = new LoginRequest("testuser", "password");
        User user = new User("testuser", "test@example.com", new BCryptPasswordEncoder().encode("password"));

        when(userService.findByUsername("testuser")).thenReturn(user);
        when(userService.checkPassword("password", user.getPassword())).thenReturn(true);
        when(jwtUtil.generateToken("testuser")).thenReturn("token");

        ResponseEntity<?> response = authController.login(request);

        assertEquals(200, response.getStatusCodeValue());
        AuthResponse authResponse = (AuthResponse) response.getBody();
        assertNotNull(authResponse);
        assertEquals("token", authResponse.getToken());
    }
}