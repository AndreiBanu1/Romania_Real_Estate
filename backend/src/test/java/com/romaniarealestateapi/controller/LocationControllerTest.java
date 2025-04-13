package com.romaniarealestateapi.controller;

import com.romaniarealestateapi.model.Location;
import com.romaniarealestateapi.service.LocationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Optional;

import static org.mockito.Mockito.when;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
class LocationControllerTest {

    @Autowired
    private LocationController locationController;

    @MockitoBean
    private LocationService locationService;

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(locationController).build();
    }

    @Test
    void testGetLocationById() throws Exception {
        Location location = new Location();
        location.setCity("City A");
        location.setProvince("Province X");

        when(locationService.getLocationById(1L)).thenReturn(Optional.of(location));

        mockMvc.perform(get("/api/locations/1"))
                .andExpect(status().isOk());

        verify(locationService).getLocationById(1L);
    }
}
