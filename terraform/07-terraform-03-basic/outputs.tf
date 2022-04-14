output "yandex_zone" {
  value       = yandex_compute_instance.vm-id[*].zone
  description = "Регион Яндекса, в котором создан инстанс"
}

output "yandex_private_ip" {
  value       = yandex_compute_instance.vm-id[*].network_interface.0.ip_address
  description = "Внутренний IP на Яндексе"
}

output "vm_public_ip" {
  value       = yandex_compute_instance.vm-id[*].network_interface.0.nat_ip_address
  description = "Внешний IP-адрес ВМ"
}