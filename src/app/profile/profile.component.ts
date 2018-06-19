import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  name = '';
  lastName = '';
  instagram = '';
  memberSince = '';
  title = 'Profile';

  // tiles = [
  //   {text: 'Campaign One', cols: 1, rows: 1, color: 'lightblue'},
  //   {text: 'Campaign Two', cols: 1, rows: 1, color: 'lightgreen'},
  //   {text: 'Campaign Three', cols: 1, rows: 1, color: 'lightpink'},
  //   {text: 'Campaign Four', cols: 1, rows: 1, color: '#DDBDF1'},
  // ];

  campaigns = [
    {title: "Campaign 1", companyName: "ABC Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 2", companyName: "XYZ Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 3", companyName: "CDE Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 4", companyName: "NOP Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."},
    {title: "Campaign 5", companyName: "NOP Company", img: "https://material.angular.io/assets/img/examples/shiba2.jpg", content: 
      "The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan. "
      + "A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was originally "
      + "bred for hunting."}
  ];

  constructor() { }

  ngOnInit() {
    console.log("test");
    // There will be a service call here. Most likely a subscribe.
    this.name = 'Pablo';
    this.lastName = 'Prieto';
    this.instagram = 'instagram.com/Pablo';
    this.memberSince = '06/07/2018';
  }

}
