package com.campaignwebapp.demo;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Collection;
import java.util.stream.Collectors;

@RestController
class CampaignController {
    private CampaignRepository repository;

    public CampaignController(CampaignRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/campaigns")
    @CrossOrigin(origins = "http://localhost:4200")
    public Collection<Campaign> campaigns() {
        return repository.findAll().stream()
                .filter(this::isCool)
                .collect(Collectors.toList());
    }

    private boolean isCool(Campaign campaign) {
        return !campaign.getName().equals("AMC Gremlin") &&
                !campaign.getName().equals("Triumph Stag") &&
                !campaign.getName().equals("Ford Pinto") &&
                !campaign.getName().equals("Yugo GV");
    }
}