delete_services:
	kubectl delete -f auth/manifests
	kubectl delete -f authdb/manifests
	kubectl delete -f converter/manifests
	kubectl delete -f gateway/manifests
	kubectl delete -f mediadb/manifests
	kubectl delete -f queue/manifests

apply_services:
	kubectl apply -f auth/manifests
	kubectl apply -f authdb/manifests
	kubectl apply -f converter/manifests
	kubectl apply -f gateway/manifests
	kubectl apply -f mediadb/manifests
	kubectl apply -f queue/manifests

reapply_services:
	delete_services
	apply_services
