theory Buffers
imports Main DataTypes
begin

(* helper *)
primrec remove_nth :: "nat => 'a list \<Rightarrow> 'a list" where
"remove_nth n [] = []" |
"remove_nth n (x # xs) = (case n of 0 \<Rightarrow> xs | Suc m \<Rightarrow> x # remove_nth m xs)"


record buffer =
  messages :: "msg list"
  leaky :: bool

definition write_message :: "'a buffer_scheme \<Rightarrow> msg \<Rightarrow> 'a buffer_scheme" where
"write_message b m = b\<lparr>messages :=  m # ( messages b)\<rparr>" 

definition clock_message :: "'a buffer_scheme \<Rightarrow> nat \<Rightarrow> (msg \<times>'a buffer_scheme) option" where
"clock_message b n = (if n \<ge> length (messages b) then None 
else messages b ! n, b\<lparr>messages := remove_nth n (messages b)\<rparr>)"



(* So now there should be a leaky buffer 
whose only property is that it can house even more functions.
 Wouldn't that make
more sense to provide as another record field?
 Like, leaky :: bool, and if it's true, then we can do extra stuff *)


(*What's up with the structure of peek_message? *)
(* definition peek_message :: "'a buffer_scheme \<Rightarrow> nat \<Rightarrow> msg" where
"peek_message b n = leak_function messages b ! n"

definition leak_function :: "msg \<Rightarrow> msg"*)

end
