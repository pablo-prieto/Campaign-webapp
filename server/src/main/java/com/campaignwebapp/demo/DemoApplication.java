package com.campaignwebapp.demo;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import java.util.stream.Stream;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @Bean
    ApplicationRunner init(CampaignRepository repository) {
        return args -> {
            Stream.of("Audi", "Mercedes", "Porsche", "Lamborghini", "Bugatti",
                      "AMC Gremlin", "Triumph Stag", "Ford Pinto", "Nissan").forEach(name -> {
                Campaign campaign = new Campaign();
                campaign.setName(name);
                repository.save(campaign);
            });
            repository.findAll().forEach(System.out::println);
        };
    }
}
