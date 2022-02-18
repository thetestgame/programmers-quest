##########################################################################
# quest-dev.prc                                                          #
#                                                                        #
# This file defines the the panda runtime configuration values           #
# used by development copies of the Programmers Quest MMORPG             #
##########################################################################

# Network:

# Due to a bug with Astron's DC parser implementation we need to manually
# match the DC hash across client/server. This value should match that found
# in the Astron configuration file
manual-dc-hash 0xDEADBEEF