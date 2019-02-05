package com.campaignwebapp.demo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource
interface CampaignRepository extends JpaRepository<Campaign, Long> {
}