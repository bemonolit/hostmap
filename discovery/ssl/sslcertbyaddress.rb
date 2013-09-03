require 'set'
require 'plugins'
begin
require 'net/https'
rescue Exception
  $LOG.warn "Missing library OpenSSL, please install libopenssl-ruby."
end


#
# Simple work around to avoid messagges "warning: peer certificate won't be verified in this SSL session".
#
class Net::HTTP

  alias_method :old_initialize, :initialize

  def initialize(*args)
    old_initialize(*args)
    begin
      @ssl_context = OpenSSL::SSL::SSLContext.new
      @ssl_context.verify_mode = OpenSSL::SSL::VERIFY_NONE
    rescue
      @ssl_context = nil
    end
  end
end

#
# Check the X.509 certificate from the web server.
#
class HostmapPlugin < Hostmap::Plugins::BasePlugin

  def info
    {
      :name => "SSLCertByAddress",
      :author => "Alessandro Tanasi",
      :version => "0.3",
      :require => :ip,
      :description => "Check the X.509 certificate from the web server."
    }
  end

  def execute(ip, opts = {})
    # Configuration check
    if opts['onlypassive']
      $LOG.warn "Skipping SSL because only passive checks are enabled"
      return @res
    end

    opts['httpports'].split(',').each do |port|
      begin
        http = Net::HTTP.new(ip, port.to_i)
        http.use_ssl = true

        @cns = []
      
        http.start() do |conn|
          cert = OpenSSL::X509::Certificate.new conn.peer_cert
          # Get data from issuer CN field
          cert.issuer.to_a.each{|oid, value|
            @cns << value if oid == "CN"
          }
          # Get data from subject CN field
          cert.subject.to_a.each{|oid, value|
            @cns << value if oid == "CN"
          }
          cert.extensions.each { |ext|
            # Fucking hack because OpenSSL::X509::Extension documentation is missing
            if ext.to_s =~ /^subjectAltName =/
              ext.to_s.gsub(/^subjectAltName = /, '').split(',').each do |cn|
                  @cns << cn.downcase.split('dns:')[1] if cn.downcase =~ /^dns:/
              end
            end
          }
        end
      rescue Exception
        next
      end
     
      # Checks if is a wildcard certificate
      @cns.each do |cn|
        if cn =~ /^\*\./
          $LOG.warn "Detected a wildcard entry in X.509 certificate for: #{cn}"
          next
        else
          @res << { :hostname => cn } if !cn.nil?
        end
      end
    end

    return @res
  end
end
