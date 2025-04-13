package com.romaniarealestateapi.service;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.romaniarealestateapi.exception.ResourceNotFoundException;
import com.romaniarealestateapi.model.Property;
import com.romaniarealestateapi.repository.PropertyRepository;

@Service
public class PropertyService {
    private final PropertyRepository propertyRepository;
    
    @Autowired
    public PropertyService(PropertyRepository propertyRepository) {
        this.propertyRepository = propertyRepository;
    }

    public List<Property> getAllProperties() {
        return propertyRepository.findAll();
    }

    public Property getPropertyById(Long id) {
        return propertyRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Property not found with id: " + id));
    }

    public Property saveProperty(Property property) {
        return propertyRepository.save(property);
    }

    public void deleteProperty(Long id) {
        propertyRepository.deleteById(id);
    }
}
