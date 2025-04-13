package com.romaniarealestateapi.controller;

import java.util.List;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.romaniarealestateapi.model.Agency;
import com.romaniarealestateapi.service.AgencyService;
import com.romaniarealestateapi.exception.ResourceNotFoundException;

@RestController
@RequestMapping("/api/agencies")
@CrossOrigin(origins = "*") // Allow frontend requests
public class AgencyController {
    private final AgencyService agencyService;

    @Autowired
    public AgencyController(AgencyService agencyService) {
        this.agencyService = agencyService;
    }

    @GetMapping
    public List<Agency> getAllAgencies() {
        return agencyService.getAllAgencies();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Agency> getAgencyById(@PathVariable Long id) {
        try {
            Agency agency = agencyService.getAgencyById(id);
            return ResponseEntity.ok(agency); // 200 OK
        } catch (ResourceNotFoundException ex) {
            return ResponseEntity.notFound().build(); // 404 Not Found
        }
    }

    @PostMapping
    public Agency createAgency(@Valid @RequestBody Agency agency) {
        return agencyService.createAgency(agency);
    }
}
