# Autonomous Parking


The aim of the project is to create three different models for autonomous parking.

* Genetic algorithm
* NEAT algorithm
* Reinforcement learning - PPO 
* Fuzzy sets [In the future]

Run the program
 ```
python main.py
```

genome_array holds genome for each car in the population. Each car genome holds information about neural network weights for each connection between neural layers.


# To run one specific test 

`python3 -m unittest tests.test_genetic_helper.TestGeneticHelper.test_mutate_ieee_754_genome_with_low_probability`

# To run all tests 

`python3 -m unittest discover tests`
