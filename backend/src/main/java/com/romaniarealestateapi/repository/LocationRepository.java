package com.romaniarealestateapi.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.romaniarealestateapi.model.Location;

public interface LocationRepository extends JpaRepository<Location, Long> {

    Location findByCity(String city);
    Location findByProvince(String province);
    Location findByNeighborhood(String neighborhood);

    boolean existsByCity(String city);
    boolean existsByProvince(String province);
}

    
