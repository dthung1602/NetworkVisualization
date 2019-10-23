# Network Visualization
## 1. Introduction
### 1.1 Purpose  
Communication networks grow both in quantity and quality. In the past decades, the
amount of communication-enabled devices increased massively while also the required
quality of networks increased. Thus, monitoring, administration and management of
communication networks has become a challenging task for network providers which
requires a state-of-the-art set of tools.
A first step towards intelligent network management is an adequate monitoring. Due
to the massive amount of different parameters and attributes of communication networks,
e.g., performance, online/offline notifications, reliability, robustness, and/or security,
monitoring becomes a complex task. One way to support network administrators is
to use proper visualization methods of network information in order to provide a swift
overview about possible problems. 
### 1.2 Goal
2 Goal
As a first step it is important to identify relevant
properties in a communication network
and derive a model from an actual instance.
Then, this model is to be used as input to a
tool that is creating a visualization of the network
and its properties as output. The major
task of this course is to design, implement
and evaluate this tool and write down the results
in a scientific report. You will work in
teams and gain team communication and (selfresponsible)
management competencies during
the project while making intelligent (software
design/implementation) decisions.
## 2. Functionalities
### 2.1 Basic Functionalities
- Open graph: The user can open a graph in .graphml format by clicking on “File → Open” in the menu or using the hotkey “Ctrl+O”.
-	Save graph: The user can save the new graph as .graphml file by clicking on “File → Save” in the menu or using the hotkey “Ctrl+S”.
-	Save as image: The user can save the current graph as an image (.png or .jpg) by clicking on “File → Save image” in the menu or using the hotkey “Ctrl+Shift+S”
-	Add vertex: The user can add a new vertex by clicking on the “Add vertex” button, then click on the desired position on the graph.
-	Delete vertex: The user can delete a vertex by clicking on the “Delete vertex” button, then click on the desired vertex.
-	Add edge: The user can add a new edge by clicking on the “Add edge” button, then click on 2 vertices.
-	Delete edge: The user can delete an edge by clicking on the “Delete edge” button, then click on the desired edge.
-	Drag vertices: The user can click on a vertex, then drag it to the new position.
-	Drag background: The user can drag the background to move the viewport.
-	Zoom in/out of the graph: The user can scroll the mouse wheel or click on the zoom buttons on the toolbar to adjust the viewport zoom.
-	View/edit the attributes of vertices/edges: To view the attributes of a vertex/ an edge, the user can click on it. The attributes will be displayed on the right panel of the app where the user can edit them.
-	Add attributes to vertices/edges: To add new attributes to the graph, the user can click on the “Add new attribute” button on the toolbar, then select the attribute name and whether the attribute should be added to vertices or edges.
(Note: before adding/deleting a vertex/an edge, edit mode has to be activated by clicking the “Edit” button in the toolbar)
### 2.2 Check for missing attributes
When importing a graph, we expect its vertices and edges to contain some basic attributes. However, not all graphs satisfy this condition and this is the motivation for this function.
### 2.3 Geographical view
The application provides users a way to visualize the geolocations of the hosts in the network. 
### 2.4 Change graph layout
In many cases, the geolocation of the hosts is not very useful but the topology of the network may display many interesting properties. The application can apply different layout algorithms to the network to enhance its understandability and usability.
### 2.5 Display vertex centrality
The application can use color to visualize the centrality of the vertices, with cooler colors for lower centrality and warmer colors for higher centrality.
### 2.6 Filter edges
The graph occasionally contains too many edges which makes the graph hard to be observed. This function provides the user with a proper way to view the desired edges based on their values.
### 2.7 Find the shortest path
Finding the shortest path between vertices can help to optimize the performance of the network.
### 2.8 Find clusters
Finding clusters of a network provide more insights for users into the particular network, as it groups the separated vertices of the original network into a set of non-overlapping groups that are densely connected internally. This can help to reduce the complexity of monitoring the network if we consider each cluster as a single host.
### 2.9 Find bottleneck function
There are possibilities that a group of hosts is connected to the rest of the network by only a single link (a bottleneck). This may affect the performance of the whole network and should an error happens to the link, the group becomes isolated. The intention of this function is to identify and visualize all bottlenecks in the network.
### 2.10 Real-time mode
In reality, many properties of the network change over time and we wish to visualize those changes. However, since no real-time network data is available, in this prototype we decided to randomize the data to simulate the rapid changes of the real world.
### 2.11 Export statistical information
The Export Statistical Information function is used for summarizing, generating and visualizing information extracted from the graph. 
