# Item Catalog Project 
##(Under Udacity Full Stack Nanodegree Term-II)

### Project Overview
> To develop a web application that includes a list of categories and items, where user can add, update and delete the items once they are logged in. Each item is added under a specific category with a brief description. 

### What Will I Learn?
  * Develop a RESTful web application using the Python framework Flask
  * Implementing third-party OAuth authentication.
  * Implementing CRUD (create, read, update and delete) operations.
  
### How to Run?

#### PreRequisites
  * [Python ~3.6](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)
  
#### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Find the catalog folder and replace it with the content of the provided zip folder.

#### Launch Project
  1. Launch the Vagrant VM using command:
  
  ```
    $ vagrant up
  ```

2. Log In to the Vagrant VM using command:
  
  ```
    $ vagrant ssh
  ```
3. Run your application within the VM
  
  ```
    $ python /vagrant/catalog/project.py
  ```
4. Access and test your application by visiting [http://localhost:8000](http://localhost:8000).


#### Reference
>The credit for oauth integration and the basic implementation of the project goes to the Udacity Full Stack Nanodegree Term-II.

##### Recommendation
>To learn how to develop and build the web application and various new technologies join Udacity nanodegree programs.