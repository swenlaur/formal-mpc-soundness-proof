theory BasicState
  imports
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
    AdversarialAction
    ProtocolParty
    StandardFunctionality
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/network_components/Functionality"
begin

record  system_state =
  state_protocol_parties ::  "(party_id, protocol_party) map"
  state_functionalities ::  "(functionality_id, functionality) map"
  state_corrupted_parties :: "party_id set"
  state_outgoing_signals :: "(party_id \<times> functionality_id * instance_label * instance_label, bool) map"
  state_previous_action :: adv_action
  state_flag :: bool

end