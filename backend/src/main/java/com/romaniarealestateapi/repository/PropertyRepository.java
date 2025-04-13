package com.romaniarealestateapi.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import com.romaniarealestateapi.model.Property;

public interface PropertyRepository extends JpaRepository<Property, Long> {

    List<Property> findByCity(String city);

    List<Property> findByPriceLessThanEqual(Double price);
    
    List<Property> findByPricePerSqmLessThanEqual(Double price);

    List<Property> findByRooms(String rooms);

    List<Property> findByAgencyId(Long agencyId);
}
