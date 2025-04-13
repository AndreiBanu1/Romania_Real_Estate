package com.romaniarealestateapi.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import com.romaniarealestateapi.model.Property;

public interface PropertyRepository extends JpaRepository<Property, Long> {

    List<Property> findByCity(String city);

    List<Property> findByPriceLessThanEqual(Double price);
    
    List<Property> findByPriceSQMLessThanEqual(Double priceSQM);

    List<Property> findByNoRooms(String noRoooms);

    List<Property> findByAgencyId(Long agencyId);
}
