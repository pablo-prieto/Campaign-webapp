import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Router, ActivatedRoute } from '@angular/router';
import { CampaignService } from '../services/campaign.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  title = 'Home Page';
  returnUrl: string;
  tabProfileOpen = false;
  edibles = [];
  boroughs = [];
  filterCriteria = {};
  criteriaColor = '#FED7B5';

  campaignsInFilter = [];

  oldCampaigns = [
    {title: 'Campaign 1', id: 'campaign1', filters: ['burger'], companyName: 'ABC Company', img: '../assets/img/burger.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 2', id: 'campaign2', filters: ['ice cream'], companyName: 'DEF Company', img: '../assets/img/ice_cream2.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 3', id: 'campaign3', filters: ['chicken waffles'], companyName: 'GHI Company', img: '../assets/img/chicken_waffles.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 4', id: 'campaign4', filters: ['french fries'], companyName: 'JKL Company', img: '../assets/img/french_fries.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 5', id: 'campaign4', filters: ['fried chicken'], companyName: 'JKL Company', img: '../assets/img/fried_chicken.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 6', id: 'campaign4', filters: ['ice cream'], companyName: 'JKL Company', img: '../assets/img/ice_cream.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 7', id: 'campaign4', filters: ['burger'], companyName: 'JKL Company', img: '../assets/img/burger2.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 8', id: 'campaign4', filters: ['pizza'], companyName: 'JKL Company', img: '../assets/img/pizza.png', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'}
  ];

  // Needs to be changed to receive data from an Observable and populate accordingly
  // i.e
  // import { CarService } from '../shared/car/car.service';

  // export class CarListComponent implements OnInit {
  //   cars: Array<any>;

  //   constructor(private carService: CarService) { }

  //   ngOnInit() {
  //     this.carService.getAll().subscribe(data => {
  //       this.cars = data;
  //     });
  //   }
  // }

  campaigns = [
    {title: 'Campaign 1', id: 'campaign1', filters: ['burger'], companyName: 'ABC Company', img: '../assets/img/burger.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 2', id: 'campaign2', filters: ['ice cream'], companyName: 'DEF Company', img: '../assets/img/ice_cream2.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 3', id: 'campaign3', filters: ['chicken waffles'], companyName: 'GHI Company', img: '../assets/img/chicken_waffles.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 4', id: 'campaign4', filters: ['french fries'], companyName: 'JKL Company', img: '../assets/img/french_fries.jpg', content: 
      'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 5', id: 'campaign4', filters: ['fried chicken'], companyName: 'JKL Company', img: '../assets/img/fried_chicken.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 6', id: 'campaign4', filters: ['ice cream'], companyName: 'JKL Company', img: '../assets/img/ice_cream.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 7', id: 'campaign4', filters: ['burger'], companyName: 'JKL Company', img: '../assets/img/burger2.jpg', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'},
    {title: 'Campaign 8', id: 'campaign4', filters: ['pizza'], companyName: 'JKL Company', img: '../assets/img/pizza.png', content: 
    'This restaurant/business offers x, y and z to participants who register for our event and promote our product.'}
  ];

  constructor(
    private router: Router, private route: ActivatedRoute, private campaignService: CampaignService
  ) { }

  ngOnInit() {
    this.retrieveFilterCriteria();
    this.campaignService.getAll().subscribe(data => {
      console.log('localhost data: ', data);
    });
  }

  toggleProfile() {
    this.tabProfileOpen = !this.tabProfileOpen;
  }

  openCampaign(id) {
    console.log('campaign ID: ', id);
    this.router.navigate(['main/campaignDetails/' + id]);
  }

  retrieveFilterCriteria() {
    //Call some backend service to retrive the criterias for the user.
    this.filterCriteria = {
      'edibles' : [ 'Burgers', 'Pizza', 'Vegan', 'Medicine', 'Fried Chicken', 'Ice Cream', 'French Fries' ],
      'boroughs' : {
        'Manhattan': [ 'Upper West Side', 'Upper East Side', 'Harlem', 'Washington Heights', 'Spanish Harlem'],
        'Queens' : [],
        'Brooklyn': [],
        'Staten Island': [],
        'Bronx': []
      }
    }

    this.edibles = this.filterCriteria['edibles'];
    console.log('retrieveFilterCriteria: ', this.filterCriteria);
    for (let borough in this.filterCriteria['boroughs']) {
      console.log('borough: ', borough);
      this.boroughs.push(borough);
    }
  }

  filterCampaigns(criteria) {
    // Filters are changing order even when they are the same, need to find a way to make sure it knows it's the same filter.
    console.log('criteria: ', criteria);
    let currentCampaigns = this.campaignsInFilter;
    let filteredCampaigns = [];
    for (let innerCampaign of this.oldCampaigns) {
      if(this.filterItems(criteria, innerCampaign.filters).length > 0) {
        filteredCampaigns.push(innerCampaign);
      }
    }
    this.campaignsInFilter = filteredCampaigns;
    console.log('filteredCampaigns: ', filteredCampaigns);
    console.log('currentCampaigns: ', currentCampaigns);
    this.campaigns = filteredCampaigns.concat(currentCampaigns);
  }

  filterItems(query, filters) {
    return filters.filter((el) =>
      el.toLowerCase().indexOf(query.toLowerCase()) > -1
    );
  }

  clearEdibles() {
    this.campaigns = this.oldCampaigns;
    this.campaignsInFilter = [];
  }

  clearBoroughs() {

  }

}
