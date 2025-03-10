package com.pricebyte.prerelease.service;

import com.pricebyte.prerelease.entity.User;
import com.pricebyte.prerelease.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    private BCryptPasswordEncoder passwordEncoder;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        passwordEncoder = new BCryptPasswordEncoder();
    }

    @Test
    void testRegisterUser() {
        String username = "testuser";
        String email = "test@example.com";
        String password = "password";

        when(userRepository.existsByUsername(username)).thenReturn(false);
        when(userRepository.existsByEmail(email)).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(new User(username, email, passwordEncoder.encode(password)));

        User user = userService.registerUser(username, email, password);

        assertNotNull(user);
        assertEquals(username, user.getUsername());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void testRegisterUserAlreadyExists() {
        String username = "testuser";
        String email = "test@example.com";
        String password = "password";

        when(userRepository.existsByUsername(username)).thenReturn(true);

        assertThrows(RuntimeException.class, () -> userService.registerUser(username, email, password));
    }
}