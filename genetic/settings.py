settings = {
  # To initialize same search space, use the same seed for random operations
  # 1086, 4252
  'random_seed':                                      1086,
              ############ CHROMOSOME REPRESENTATION ############
  # 'binary','float', 'int'
  'chromosome_representation':                        'float',
  'chromosome_representation_options':                ['binary', 'float', 'int'],
  'binary_number_bits':                               6,
  'int_number_range':                                 [-30, 30],
  'float_number_range':                               [-5, 5],

                    ############ NEURAL NETWORK ############
  # Range for initializing weights and biases
  # For int representation
  'int_weight_init_mean':                              0,
  'int_weight_init_stdev':                             10,

  # For float representation
  'float_weight_init_mean':                            0.0,
  'float_weight_init_stdev':                           1.0,


                    ############ BREED ############
  # default, segments
  'breeding_method':                                  'default',
  # Copy the best chromosome from the previous population to the new population
  'add_previous_best':                                False,

                    ############ MUTATION ############
  'mutation_probability':                             0.15,

  # default, gaussian
  'mutation_method':                                  'gaussian',

  # For int representation
  'int_default_mutation_range':                       [-5, 5],

  'int_gaussian_mutation_mean':                       0,
  'int_gaussian_mutation_stdev':                      5,
  
  # For float representation
  'float_default_mutation_range':                     [-0.20, 0.20],

  'float_gaussian_mutation_mean':                     0.0,
  'float_gaussian_mutation_stdev':                    0.6,

                    ############ SELECTION ############
  # roulette, tournament
  'selection_method':                                 'tournament',
  'tournament_procentage':                            0.001,
  'tournament_size':                                  10,
                    ############ POPULATION ############
  'population_size':                                  32,
                    ############ CROSSOVER  ############
  'crossover_probability':                            0.8,

}
