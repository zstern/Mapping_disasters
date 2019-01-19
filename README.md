### ImageGEO: A collaboration between New Light Technologies and General Assembly's Team Street View

[New Light Technologies](https://www.newlight.com/) (NLT) is an organization founded in 2003. They are on a mission to make the world more environmentally friendly, have developed an innovative carbon capture technology,  and do contracting work with various organizations, including FEMA (the Federal Emergency Management Agency), the U.S. Census Bureau, and The World Bank.

[Ran Goldblatt](https://www.linkedin.com/in/ran-goldblatt-34365886/), our contact with NLT, is a remote sensing scientist and senior consultant. He has a strong background in geographic information systems (GIS) and leverages this knowledge when solving problems facing various agencies.

Team Street View is a data science-based team at [General Assembly](https://generalassemb.ly/) (GA). We draw our experiences from a diversity of backgrounds and industry experiences and are collaborating with NLT on a specific task of interest for which we have created the ImageGEO tool.

Our team is [Hussain Burhani](https://www.linkedin.com/in/hussain-burhani/), [Nick Gayliard](https://www.linkedin.com/in/nick-gayliard/), [Maurie Kathan](https://www.linkedin.com/in/maurie-kathan-17b67040/), and [Zack Stern](https://www.linkedin.com/in/zachary-j-stern/).


### Problem statement

During the recovery phase immediately following a disaster, the Federal Emergency Management Agency (FEMA) performs damage assessment “on the ground” to assess the level of damage caused to residential parcels and to critical infrastructure. To assure an accurate estimation of the damage, it is important to understand the condition of the structures prior to the event. 

To help and guide the damage assessment efforts following a disaster and to assist the surveyors identify the structures of interest, this tool (a web-app or a mobile app) will expect to get, as an input, a list of addresses. It will retrieve screen shots of the structures from Google Street View. The students will design a damage assessment form, which, in addition to relevant information about the level of damage to the structures, will also provide a pre-event photo of the assessed structure.


### Usage scenario

Samantha is a disaster assessment agent at FEMA, heading to the field, days after a disaster. Her office is short on resources and all she has with her is a smart phone. Yet she has been tasked to quickly scan the disaster zone and assess the damage to residential property.

She jumps out of her truck, starts walking the street, and sees the first house in disrepair. She pulls out her phone, opens the ImageGEO app, and takes a photograph facing the house. Upon taking the photograph she sees a page displaying the photo she took, the image of the home prior to the disaster, a map location, a value estimate of the house, as well as pertinent information regarding number of stories, bedrooms, and square footage, to give the complete summary of that particular property. 

At the backend, each photograph she takes is stored, along with the summary information, and available to be accessed at a later time or when web connectivity is available again. However, the idelaly, even with limited web connectivity, a low-resolution image can be uploaded directly in real-time to the disaster response team at the home office. This data can be aggregated to assess total damage and real-time statistics can be relayed to appropriate agencies for assessment, disaster management, and appropriation purposes.

In addition, the information collated can be sent to insurance companies, the tool made accessible for crowd-sourcing to allow individuals to self-report information, or simply be used through entering address information to gather pre-disaster summaries for the property.


### Under the hood

Currently, ImageGEO is in its development stage, built as a web app using Python, associated APIs, and the Flask/Dash web framework. Two different instances have been developed showcasing the variations in user experience, to use in future A/B testing. 


### Data


### Further improvements
- Deploy as a stand-alone app
- Cross-platform functionality 
- Collaborate with UX/Web-dev teams to enhance user experience
- Database engine for larger-scale 