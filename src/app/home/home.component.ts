import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  title = 'Home Page';
  returnUrl: string;
  tabProfileOpen = false;
  campaigns = [
    {title: "Campaign 1", id: "campaign1", companyName: "ABC Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 2", id: "campaign2", companyName: "XYZ Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 3", id: "campaign3", companyName: "CDE Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 4", id: "campaign4", companyName: "NOP Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."}
  ];

  constructor(
    private router: Router, private route: ActivatedRoute,
  ) { }

  ngOnInit() {
  }

  toggleProfile() {
    this.tabProfileOpen = !this.tabProfileOpen;
  }

  openCampaign(id) {
    console.log('campaign ID: ', id);
    this.router.navigate(['main/campaignDetails/' + id]);
  }

}
