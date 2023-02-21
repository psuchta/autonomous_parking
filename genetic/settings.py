settings = {
              ############ CHROMOSOME REPRESENTATION ############
  # 'binary','float', 'int'
  'chromosome_representation':                        'float',
  'chromosome_representation_options':                ['binary', 'float', 'int'],
  'binary_number_bits':                               7,
  'int_number_range':                                 [-30, 30],
  'float_number_range':                               [-15, 15],

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
  'add_previous_best':                                True,

                    ############ MUTATION ############
  'mutation_probability':                             0.01,

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
  'tournament_size':                                  15,
                    ############ POPULATION ############
  'population_size':                                  32,
                    ############ CROSSOVER  ############
  # single, multiple
  'crossover_method':                                 'single',
  'crossover_probability':                            0.8,

}
