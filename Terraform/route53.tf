# Create Route 53 Hosted Zone
resource "aws_route53_zone" "main" {
  name = "myapp.com"
}

# Create DNS Record
resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.main.zone_id
  name = "app.myapp.com"
  type = "A"
  alias {
    name = aws_lb.app.dns_name
    zone_id = aws_lb.app.zone_id
    evaluate_target_health = true
  }
}
