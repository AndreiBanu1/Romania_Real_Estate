package com.romaniarealestateapi.service;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.romaniarealestateapi.exception.ResourceNotFoundException;
import com.romaniarealestateapi.model.Agency;
import com.romaniarealestateapi.repository.AgencyRepository;

@Service
public class AgencyService {
    private final AgencyRepository agencyRepository;
    
    @Autowired
    public AgencyService(AgencyRepository agencyRepository) {
        this.agencyRepository = agencyRepository;
    }

    public List<Agency> getAllAgencies() {
        return agencyRepository.findAll();
    }

    public Agency getAgencyById(Long id) {
        return agencyRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Agency not found with id " + id));
    }

    public Agency createAgency(Agency agency) {
        return agencyRepository.save(agency);
    }
}
