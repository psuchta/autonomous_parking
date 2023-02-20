settings = {
              ############ CHROMOSOME REPRESENTATION ############
  # 'binary','float', 'int'
  'chromosome_representation':                        'float',
  'chromosome_representation_options':                ['binary', 'float', 'int'],
  'binary_number_bits':                               5,
  'int_number_range':                                 [-15, 15],
  'float_number_range':                               [-1, 1],

                    ############ BREED ############
  # default, segments
  'breeding_method':                                  'default',
  # Copy the best chromosome from the previous population to the new population
  'add_previous_best':                                False,
                    ############ MUTATION ############
  'mutation_probability':                             0.1,
  # default, gaussian
  'mutation_method':                                  'default',
  'int_mutation_range':                               [-1, 1],
  'float_mutation_range':                             [-0.15, 0.15],
  # scale at which guassian random number will be multiplayed by
  # random number within range specified in 'int_mutation_range' or 'float_mutation_range' will be multiplied by 'mutation_scale'
  'mutation_scale':                                   0.2,
                    ############ SELECTION ############
  # roulette, tournament
  'selection_method':                                 'tournament',
  'tournament_procentage':                            0.3,
                    ############ POPULATION ############
  'population_size':                                  32,
                    ############ CROSSOVER  ############
  'crossover_probability':                            0.6,

}
