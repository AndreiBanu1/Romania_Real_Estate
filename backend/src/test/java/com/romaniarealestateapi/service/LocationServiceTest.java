package com.romaniarealestateapi.service;

import com.romaniarealestateapi.model.Location;
import com.romaniarealestateapi.repository.LocationRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class LocationServiceTest {

    @Mock
    private LocationRepository locationRepository;

    @InjectMocks
    private LocationService locationService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testGetLocationById() {
        Location location = new Location();
        location.setCity("City A");
        location.setProvince("Province X");

        when(locationRepository.findById(1L)).thenReturn(Optional.of(location));

        Optional<Location> result = locationService.getLocationById(1L);

        assertTrue(result.isPresent());
        assertEquals("City A", result.get().getCity());
    }
}
