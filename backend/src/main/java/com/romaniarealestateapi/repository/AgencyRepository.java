package com.romaniarealestateapi.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.romaniarealestateapi.model.Agency;

public interface AgencyRepository extends JpaRepository<Agency, Long> {

    Agency findByExternalId(Integer externalId);

    boolean existsByName(String name);
}
