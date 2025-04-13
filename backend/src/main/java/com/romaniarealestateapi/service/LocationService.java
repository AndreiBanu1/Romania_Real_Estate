package com.romaniarealestateapi.service;

import com.romaniarealestateapi.model.Location;
import com.romaniarealestateapi.repository.LocationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LocationService {

    private final LocationRepository locationRepository;

    // Constructor injection for LocationRepository
    @Autowired
    public LocationService(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    // Method to get all locations
    public List<Location> getAllLocations() {
        return locationRepository.findAll();
    }

    // Method to get a location by ID
    public Optional<Location> getLocationById(Long id) {
        return locationRepository.findById(id);
    }

    // Method to save a new location
    public Location saveLocation(Location location) {
        return locationRepository.save(location);
    }

    // Method to delete a location by ID
    public void deleteLocation(Long id) {
        locationRepository.deleteById(id);
    }

}
